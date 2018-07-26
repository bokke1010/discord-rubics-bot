from PIL import Image, ImageDraw


# def renderCube(image):

def pointOnLine(points: list, divider: float) -> list:
    # print(points)
    startPoint = points[0]
    line = [points[1][0] - points[0][0], points[1][1] - points[0][1]]
    return [startPoint[0] + line[0] * divider, startPoint[1] + line[1] * divider]

def renderTriangle(image: Image, points: list, color = (0,0,0,0)) -> Image:
    draw = ImageDraw.Draw(image)
    print(black)
    for i in range(100):
        divider = i/100
        coords = (tuple(points[0]), tuple(pointOnLine([points[1],points[2]], divider)))
        print(coords)
        draw.line(coords, fill=color)
    return image

def renderQuad(image, points, color):
    renderTriangle(image, [points[0],points[1],points[2]], color)
    renderTriangle(image, [points[3],points[1],points[2]], color)

size = (128,128)
transparantBlue = (0,255,0, 127) # blue for now
black = (0,0,0,0) # should be black
result = Image.new('RGBA', size, transparantBlue)
renderTriangle(result, [[20,25],[30,55],[60,30]])
result.save("result.png")
