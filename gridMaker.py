import cv2
import os

def validate(inp):
    try:
        return int(inp);
    except ValueError:
        return None;

def make_grid(imgPath, rows, cols, offset, square, bnw, invert, yPrio, thickness, color):
    # Validate all integer values
    rows = validate(rows);
    cols = validate(cols);
    offset = (validate(offset[0]), validate(offset[1]));
    thickness = validate(thickness);

    if (any(ele == None for ele in [rows, cols, offset[0], offset[1], thickness])):
        return "VALUE_ERROR";

    # Read the image file
    img = cv2.imread(imgPath);
    if img.size == 0:
        return "FILE_ERROR";

    # Extract file name and extension
    outputFileName = imgPath.split("\\")[-1].split(".")[0]+"_grid";

    # Check if the image has to pass through any of the filters
    # Convert to black and white
    if bnw:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        outputFileName += "_bnw";
    # Convert to a color invert
    if invert:
        img = cv2.bitwise_not(img);
        outputFileName += "_inv";
    
    # Read dimensions of the image
    dimensions = img.shape;

    # Calculate step size for both axis
    x_step = int(dimensions[1] / cols);
    y_step = int(dimensions[0] / rows);

    # Circular shift the offset if they overflow
    x_offset = offset[0] % x_step;
    y_offset = offset[1] % y_step;

    # Check if the square option is selected
    if square:
        # Give priority to the respective axis
        if yPrio:
            x_step = y_step;
        else:
            y_step = x_step;

    # Draw vertical lines of the grid
    for x in range(x_offset, dimensions[1], x_step):
        # cv.Line(img, pt1, pt2, color, thickness=1, lineType=8, shift=0);
        img = cv2.line(img, (x, 0), (x, dimensions[0]), color, thickness);

    # Draw horizontal lines of the grid
    for y in range(y_offset + dimensions[0], 0, (-1*y_step)):
        # cv.Line(img, pt1, pt2, color, thickness=1, lineType=8, shift=0);
        img = cv2.line(img, (0, y), (dimensions[1], y), color, thickness);

    outputPath = os.path.join(".\\gridImages\\", (outputFileName +'.jpg'));
    print(outputPath);
    # Save the image
    print(cv2.imwrite(outputPath, img));

    return outputPath;