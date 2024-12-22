# Midpoint calculation (between points box[3] and box[2])
midx = (box[3][0] + box[2][0]) / 2
midy = (box[3][1] + box[2][1]) / 2  # Fix the incorrect summation for y-coordinate

cv2.circle(result_image, (int(midx), int(midy)), 5, (0, 255, 255), -1)  # Draw the centroid

# Now, we have the midpoint (midx, midy) and the centroid (cx, cy)
# Calculate the angle between the center (cx, cy) and the midpoint (midx, midy)
# angle_rad2 = np.arctan((midy - cy) / (midx - cx)) # Arctangent of the difference in y and x coordinates
angle_rad2 = np.arctan2((midy - cy), (midx - cx))  # Arctangent of the difference in y and x coordinates

angle_deg2 = angle_rad2 * 180 / np.pi  # Convert from radians to degrees

# Debug: we want to choose the shorter edge of the rotated rect to compute the angle between vertical
# https://stackoverflow.com/a/21427814/3661547
if width1 > height1:
    angle_deg2 = angle_deg2 + 180
else:
    angle_deg2 = angle_deg2 + 90

angle_rad2 = angle_deg2 * np.pi / 180
