import numpy as np
import pathlib
from PIL import Image


def decode(img_data, ix, iy):
    w = ix * iy
    assert len(img_data) % w == 0, \
        "invalid image data shape (should be a multiple of its dimensions)"
    n_layers = len(img_data) // w
    data = np.array([
        np.array(list(map(int, img_data[i * w:(i + 1) * w])),
                 dtype=np.uint8).reshape((iy, ix)) for i in range(n_layers)
    ])
    return data


def ite(cond, x, y):
    return cond * x + (1 - cond) * y


def mix(l1, l2):
    return ite(l1 >> 1, l2, l1)


def main():
    debug = False
    img = pathlib.Path('assets/day8-input').read_text().strip()
    # data = decode("123456789012", 3, 2)
    data = decode(img, 25, 6)
    scores = np.sum(np.sum(data == 0, axis=2), axis=1)
    l = np.argmin(scores)
    if debug:
        print(l)
        print(scores, scores[l])
    print("part 1:", np.sum(data[l] == 2) * np.sum(data[l] == 1))
    img = data[0]
    for l in data[1:]:
        img = mix(img, l)
    Image.fromarray(img * 255).save('day8.png')
    print("part 2: see 'xdg-open day8.png'")


if __name__ == '__main__':
    main()
