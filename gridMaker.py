# Import the required modules
import os
import cv2

# API to validate the numerical values
def validate(inp):
    # Check if the string contains int values
    try:
        return int(inp);
    # Else return None
    except ValueError:
        return None;

# API to create the grid
def make_grid(imgPath, rows=10, cols=10, offset=(0,0), square=False, bnw=False, invert=False, binary=False, rowPrio=False, thickness=1, color=(255,0,0,1)):
    # Validate all integer values
    rows = validate(rows);
    cols = validate(cols);
    offset = (validate(offset[0]), validate(offset[1]));
    thickness = validate(thickness);

    if (any(ele == None for ele in [rows, cols, offset[0], offset[1], thickness])):
        return "VALUE_ERROR";

    # Read the image file
    try:
        img = cv2.imread(imgPath);
        # Read dimensions of the image
        dimensions = img.shape;
    except:
        return "FILE_ERROR";

    # Extract file name and set it to the output folder
    outputFileName = "gridImages\\" + imgPath.split("\\")[-1].split(".")[0]+"_grid";

    # Check if the image has to pass through any of the filters
    # Convert to black and white
    if bnw or binary:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        if binary:
            (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY);
            outputFileName += "_bin";
        else:
            outputFileName += "_bnw";
    # Convert to a color invert
    if invert:
        img = cv2.bitwise_not(img);
        outputFileName += "_inv";

    # Calculate step size for both axis
    xStep = int(dimensions[1] / cols);
    yStep = int(dimensions[0] / rows);

    # Circular shift the offset if they overflow
    xOffset = offset[0] % xStep;
    yOffset = offset[1] % yStep;

    # Check if the square option is selected
    if square:
        # Give priority to the respective axis
        if rowPrio:
            xStep = yStep;
        else:
            yStep = xStep;

    # Draw vertical lines of the grid
    for x in range(xOffset, dimensions[1], xStep):
        # cv.Line(img, pt1, pt2, color, thickness=1, lineType=8, shift=0);
        img = cv2.line(img, (x, 0), (x, dimensions[0]), color, thickness);

    # Draw horizontal lines of the grid
    for y in range(yOffset + dimensions[0], 0, (-1*yStep)):
        # cv.Line(img, pt1, pt2, color, thickness=1, lineType=8, shift=0);
        img = cv2.line(img, (0, y), (dimensions[1], y), color, thickness);

    # Add the extension to the output file name
    outputFileName += ".jpg";
    # Get the current working directory of the .py file
    outputPath = os.path.dirname(os.path.abspath(__file__));
    # Save the image an return error is something goes wrong
    if not (cv2.imwrite(os.path.join(outputPath, outputFileName), img)):
        return "UNKNOWN_ERROR";

    # Return the output file path
    return os.path.join(outputPath, outputFileName);