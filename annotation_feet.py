import cv2, json, os

annotations_for_image = []

def draw_rectangle(event, x, y, flags, param):
    global drawing, xmin, ymin, xmax, ymax

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xmin, ymin = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        xmax, ymax = x, y
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        drawing = False
        nivel = input("nivel da ferida: ")
        grau = input("grau da ferida: ")
        annotations_for_image.append({
            'class_name': 'feet',
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax,
            'nivel': nivel,
            'grau': grau
        })

def annotate_feet_images(image_dir, annotation_dir):
    if not os.path.exists(annotation_dir):
        os.makedirs(annotation_dir)

    annotations = []

    for filename in os.listdir(image_dir):
        if filename.lower().endswith('.jpeg'):
            image_path = os.path.join(image_dir, filename)
            annotation_path = os.path.join(annotation_dir, filename.replace('.jpeg', '.json'))

            global annotations_for_image
            annotations_for_image = []

            global image
            image = cv2.imread(image_path)
            cv2.imshow('Image', image)
            cv2.setMouseCallback('Image', draw_rectangle)

            while True:
                cv2.imshow('Image', image)
                k = cv2.waitKey(1)

                if k == 27:
                    break
                elif k == 13:
                    annotations.append({
                        'image_path': image_path,
                        'annotations': list(annotations_for_image),
                    })
                    print(f"Annotations saved for {filename}")
                    break

            with open(annotation_path, 'w') as f:
                json.dump(annotations_for_image, f)

    with open('annotations.json', 'w') as f:
        json.dump(annotations, f)

if __name__ == '__main__':
    image_dir = 'feets'
    annotation_dir = 'annotations'

    annotate_feet_images(image_dir, annotation_dir)
