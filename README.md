# cv_toolboxes

Here some operations on Image and annotations for Text Detection, Image Segmentation, Object Detection and etc.

## How to Use?

- Judge coordinates of Polygon whether clockwise or counter-clockwise

```shell
python3 clockwise_coord.py
```

- Translate VIA tools annotation formation into ICDAR2015 annotation formation

For example,the target format like below.
```
x1,y1,x2,y2,x3,y3,x4,y4 text
```
```
python3 via2icdar15.py
```
