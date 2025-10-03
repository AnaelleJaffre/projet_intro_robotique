import numpy as np
import cv2
from image_processing.new_params import NEW_BLUE, NEW_RED, NEW_YELLOW, NEW_BROWN
from image_processing.opencv_inrange_camera_params import RED, BLUE, YELLOW, BROWN


def calibrate_color_threshold(cap, preset_low, preset_high, num_samples=10, adjustment_range=30):
    """
    Calibrates color thresholds to maximize line detection under current lighting.
    
    Args:
        cap: OpenCV VideoCapture object
        preset_low: Initial lower HSV threshold (H, S, V)
        preset_high: Initial upper HSV threshold (H, S, V)
        num_samples: Number of frames to analyze
        adjustment_range: Max adjustment per channel (in HSV units)
    
    Returns:
        Tuple of (optimized_low, optimized_high) as numpy arrays
    """
    
    print(f"Calibrating... Point camera at the line.")
    print("Press 's' to start calibration, 'q' to quit")
    
    # Wait for user to position camera
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        cv2.imshow('Position Camera - Press S to Start', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            cv2.destroyWindow('Position Camera - Press S to Start')
            break
        elif key == ord('q'):
            cv2.destroyAllWindows()
            return np.array(preset_low), np.array(preset_high)
    
    best_low = np.array(preset_low, dtype=np.uint8)
    best_high = np.array(preset_high, dtype=np.uint8)
    best_score = 0
    
    # Collect sample frames with visual feedback
    frames = []
    print(f"Collecting {num_samples} sample frames...")
    for i in range(num_samples):
        ret, frame = cap.read()
        if ret:
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frames.append(hsv_frame)
            
            # Show preview with current preset
            mask = cv2.inRange(hsv_frame, best_low, best_high)
            preview = np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
            
            cv2.putText(preview, f"Collecting samples: {i+1}/{num_samples}", 
                       (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.imshow('Calibration', preview)
            cv2.waitKey(33)  # ~30fps
    
    if len(frames) < num_samples // 2:
        print("Warning: Could not capture enough frames, using preset values")
        cv2.destroyAllWindows()
        return best_low, best_high
    
    # Test different threshold combinations
    print("Testing threshold combinations...")
    
    # Define search space around preset values
    h_low_range = range(max(0, preset_low[0] - adjustment_range), 
                        min(180, preset_low[0] + adjustment_range + 1), 2)
    h_high_range = range(max(0, preset_high[0] - adjustment_range), 
                         min(180, preset_high[0] + adjustment_range + 1), 2)
    
    s_low_range = range(max(0, preset_low[1] - adjustment_range * 2), 
                        min(255, preset_low[1] + adjustment_range * 2 + 1), 5)
    s_high_range = range(max(0, preset_high[1] - adjustment_range * 2), 
                         min(255, preset_high[1] + adjustment_range * 2 + 1), 5)
    
    v_low_range = range(max(0, preset_low[2] - adjustment_range * 2), 
                        min(255, preset_low[2] + adjustment_range * 2 + 1), 5)
    v_high_range = range(max(0, preset_high[2] - adjustment_range * 2), 
                         min(255, preset_high[2] + adjustment_range * 2 + 1), 5)
    
    # Iterative optimization: adjust one parameter at a time
    current_low = list(preset_low)
    current_high = list(preset_high)
    
    # Create a test frame for live visualization
    test_frame = cv2.cvtColor(frames[len(frames)//2], cv2.COLOR_HSV2BGR)
    test_frame_hsv = frames[len(frames)//2]
    
    iteration_count = 0
    total_iterations = 2 * 6  # 2 passes * 6 parameters
    
    # Optimize each channel
    for iteration in range(2):  # Multiple passes for refinement
        # Optimize H_low
        for h_low in h_low_range:
            test_low = np.array([h_low, current_low[1], current_low[2]], dtype=np.uint8)
            test_high = np.array(current_high, dtype=np.uint8)
            score = evaluate_threshold(frames, test_low, test_high)
            if score > best_score:
                best_score = score
                best_low = test_low.copy()
                current_low[0] = h_low
        
        iteration_count += 1
        show_calibration_progress(test_frame, test_frame_hsv, best_low, best_high, 
                                 best_score, iteration_count, total_iterations, "H_low")
        
        # Optimize H_high
        for h_high in h_high_range:
            test_low = np.array(current_low, dtype=np.uint8)
            test_high = np.array([h_high, current_high[1], current_high[2]], dtype=np.uint8)
            score = evaluate_threshold(frames, test_low, test_high)
            if score > best_score:
                best_score = score
                best_high = test_high.copy()
                current_high[0] = h_high
        
        iteration_count += 1
        show_calibration_progress(test_frame, test_frame_hsv, best_low, best_high, 
                                 best_score, iteration_count, total_iterations, "H_high")
        
        # Optimize S_low
        for s_low in s_low_range:
            test_low = np.array([current_low[0], s_low, current_low[2]], dtype=np.uint8)
            test_high = np.array(current_high, dtype=np.uint8)
            score = evaluate_threshold(frames, test_low, test_high)
            if score > best_score:
                best_score = score
                best_low = test_low.copy()
                current_low[1] = s_low
        
        iteration_count += 1
        show_calibration_progress(test_frame, test_frame_hsv, best_low, best_high, 
                                 best_score, iteration_count, total_iterations, "S_low")
        
        # Optimize S_high
        for s_high in s_high_range:
            test_low = np.array(current_low, dtype=np.uint8)
            test_high = np.array([current_high[0], s_high, current_high[2]], dtype=np.uint8)
            score = evaluate_threshold(frames, test_low, test_high)
            if score > best_score:
                best_score = score
                best_high = test_high.copy()
                current_high[1] = s_high
        
        iteration_count += 1
        show_calibration_progress(test_frame, test_frame_hsv, best_low, best_high, 
                                 best_score, iteration_count, total_iterations, "S_high")
        
        # Optimize V_low
        for v_low in v_low_range:
            test_low = np.array([current_low[0], current_low[1], v_low], dtype=np.uint8)
            test_high = np.array(current_high, dtype=np.uint8)
            score = evaluate_threshold(frames, test_low, test_high)
            if score > best_score:
                best_score = score
                best_low = test_low.copy()
                current_low[2] = v_low
        
        iteration_count += 1
        show_calibration_progress(test_frame, test_frame_hsv, best_low, best_high, 
                                 best_score, iteration_count, total_iterations, "V_low")
        
        # Optimize V_high
        for v_high in v_high_range:
            test_low = np.array(current_low, dtype=np.uint8)
            test_high = np.array([current_high[0], current_high[1], v_high], dtype=np.uint8)
            score = evaluate_threshold(frames, test_low, test_high)
            if score > best_score:
                best_score = score
                best_high = test_high.copy()
                current_high[2] = v_high
        
        iteration_count += 1
        show_calibration_progress(test_frame, test_frame_hsv, best_low, best_high, 
                                 best_score, iteration_count, total_iterations, "V_high")
    
    print(f"Calibration complete! Score: {best_score:.2f}")
    print(f"Optimized LOW:  {tuple(best_low)}")
    print(f"Optimized HIGH: {tuple(best_high)}")
    
    # Show final result
    final_mask = cv2.inRange(test_frame_hsv, best_low, best_high)
    final_preview = np.hstack([test_frame, cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)])
    cv2.putText(final_preview, "CALIBRATION COMPLETE - Press any key", 
               (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imwrite('Calibration.png', final_preview)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    
    
    return best_low, best_high


def show_calibration_progress(frame, frame_hsv, low, high, score, iteration, total, param_name):
    """Display real-time calibration progress."""
    mask = cv2.inRange(frame_hsv, low, high)
    
    # Create side-by-side display
    display = np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
    
    # Add progress information
    progress_pct = int((iteration / total) * 100)
    cv2.putText(display, f"Optimizing: {param_name} ({progress_pct}%)", 
               (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.putText(display, f"Score: {score:.2f}", 
               (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(display, f"Low: {tuple(low)}", 
               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(display, f"High: {tuple(high)}", 
               (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    # Progress bar
    bar_width = display.shape[1] - 20
    bar_height = 10
    cv2.rectangle(display, (10, display.shape[0] - 20), 
                 (10 + bar_width, display.shape[0] - 20 + bar_height), 
                 (100, 100, 100), -1)
    cv2.rectangle(display, (10, display.shape[0] - 20), 
                 (10 + int(bar_width * progress_pct / 100), display.shape[0] - 20 + bar_height), 
                 (0, 255, 0), -1)
    
    cv2.imshow('Calibration', display)
    cv2.waitKey(1)


def evaluate_threshold(frames, low, high):
    """
    Evaluates how well a threshold detects a line (maximizes contrast and compactness).
    Higher score = better line detection (darker/more defined line in threshold image).
    
    Args:
        frames: List of HSV frames
        low: Lower HSV threshold
        high: Upper HSV threshold
    
    Returns:
        Score (higher is better)
    """
    total_score = 0
    
    for frame_hsv in frames:
        # Apply threshold
        mask = cv2.inRange(frame_hsv, low, high)
        
        # Calculate metrics
        white_pixels = np.sum(mask == 255)
        total_pixels = mask.shape[0] * mask.shape[1]
        
        if white_pixels == 0:
            continue
        
        # 1. Prefer concentrated white regions (line-like)
        moments = cv2.moments(mask)
        if moments['m00'] > 0:
            # Compactness: how concentrated the white pixels are
            white_ratio = white_pixels / total_pixels
            
            # Penalize too many or too few white pixels
            # Ideal: 5-30% of frame is the line
            if 0.05 <= white_ratio <= 0.3:
                density_score = 1.0
            elif white_ratio < 0.05:
                density_score = white_ratio / 0.05
            else:
                density_score = max(0, 1.0 - (white_ratio - 0.3) / 0.5)
            
            # 2. Prefer vertical/horizontal line structure
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                # Find largest contour (should be the line)
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                if area > 50:  # Minimum area threshold
                    # Aspect ratio of bounding box
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    aspect_ratio = max(w, h) / (min(w, h) + 1)
                    
                    # Prefer elongated shapes (lines have high aspect ratio)
                    structure_score = min(1.0, aspect_ratio / 10.0)
                    
                    total_score += density_score * structure_score * 100
        
    return total_score / len(frames)


# Example usage for calibrating all colors
def calibrate_all_colors(cap):
    """
    Calibrates all color thresholds sequentially.
    """
    # Presets
    
    
    colors = {
        'RED': RED,
        'YELLOW': YELLOW,
        'BLUE': BLUE,
        'BROWN': BROWN
    }
    
    calibrated = {}
    
    for color_name, (preset_low, preset_high) in colors.items():
        print(f"\n{'='*50}")
        print(f"Calibrating {color_name}")
        print(f"{'='*50}")
        print("Position the camera to view the line clearly.")
        input("Press Enter to start calibration...")
        
        low, high = calibrate_color_threshold(cap, preset_low, preset_high)
        calibrated[color_name] = (tuple(low), tuple(high))
        
        print(f"\n{color_name} = (")
        print(f"    {calibrated[color_name][0]},  # Low")
        print(f"    {calibrated[color_name][1]}   # High")
        print(f")")
    
    return calibrated


# Main function for testing
if __name__ == "__main__":
    print("="*60)
    print("Color Threshold Calibration Tool")
    print("="*60)
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    if not cap.isOpened():
        print("ERROR: Could not open camera")
        exit()
    
    print("\nCamera initialized successfully!")
    print("Resolution: 320x240")
    
    # Define presets
    RED_PRESET = (
    (0, 140, 0),
    (180, 181, 198)
)
    YELLOW_PRESET = (
    (7, 9, 0),
    (53, 149, 255)
)
    BLUE_PRESET = (
    (94, 53, 236),
    (109, 255, 255)
)
    BROWN_PRESET = (
    (61, 5, 73),
    (180, 66, 141)
)
    
    print("\nAvailable colors to calibrate:")
    print("1. RED")
    print("2. YELLOW")
    print("3. BLUE")
    print("4. BROWN")
    print("5. ALL COLORS (sequential)")
    print("0. EXIT")
    
    while True:
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == "0":
            print("Exiting...")
            break
        
        elif choice == "1":
            print("\n" + "="*60)
            print("Calibrating RED")
            print("="*60)
            low, high = calibrate_color_threshold(cap, RED_PRESET[0], RED_PRESET[1])
            NEW_RED = (low, high)
            print(f"\nRED = (")
            print(f"    {tuple(low)},  # Low")
            print(f"    {tuple(high)}   # High")
            print(f")")
        
        elif choice == "2":
            print("\n" + "="*60)
            print("Calibrating YELLOW")
            print("="*60)
            low, high = calibrate_color_threshold(cap, YELLOW_PRESET[0], YELLOW_PRESET[1])
            NEW_YELLOW = (low, high)
            print(f"\nYELLOW = (")
            print(f"    {tuple(low)},  # Low")
            print(f"    {tuple(high)}   # High")
            print(f")")
        
        elif choice == "3":
            print("\n" + "="*60)
            print("Calibrating BLUE")
            print("="*60)
            low, high = calibrate_color_threshold(cap, BLUE_PRESET[0], BLUE_PRESET[1])
            NEW_BLUE = (low, high)
            print(f"\nBLUE = (")
            print(f"    {tuple(low)},  # Low")
            print(f"    {tuple(high)}   # High")
            print(f")")
        
        elif choice == "4":
            print("\n" + "="*60)
            print("Calibrating BROWN")
            print("="*60)
            low, high = calibrate_color_threshold(cap, BROWN_PRESET[0], BROWN_PRESET[1])
            NEW_BROWN = (low, high)
            print(f"\nBROWN = (")
            print(f"    {tuple(low)},  # Low")
            print(f"    {tuple(high)}   # High")
            print(f")")
        
        elif choice == "5":
            print("\n" + "="*60)
            print("Calibrating ALL COLORS")
            print("="*60)
            calibrated_colors = calibrate_all_colors(cap)
            
            print("\n" + "="*60)
            print("CALIBRATION RESULTS - Copy these to your code:")
            print("="*60)
            for color_name, (low, high) in calibrated_colors.items():
                print(f"\n{color_name} = (")
                print(f"    {low},  # Low")
                print(f"    {high}   # High")
                print(f")")
        
        else:
            print("Invalid choice. Please enter 0-5.")
        
        # Ask if user wants to continue
        if choice in ["1", "2", "3", "4", "5"]:
            cont = input("\nCalibrate another color? (y/n): ").strip().lower()
            if cont != 'y':
                break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nCalibration tool closed. Thank you!")