# CellVID

Turn video frames into mosaics made from Cell Machine sprites, then stitch them back into a video.

<table>
  <tr>
    <th width="50%">Bad Apple</th>
    <th width="50%">Waffle falls over</th>
  </tr>
  <tr>
    <td width="50%"><a href="https://www.youtube.com/watch?v=GOGt6hSMo48"><img src="docs/media/bad-apple.jpg" width="600" alt="Bad Apple rendered with CellVID" /></a></td>
    <td width="50%"><a href="https://www.youtube.com/watch?v=v7EoLHy85lQ"><img src="docs/media/waffle.jpg" width="600" alt="Waffle falls over rendered with CellVID" /></a></td>
  </tr>
</table>

Click a preview to watch the demo.

## Usage

The original script uses legacy Python/Pillow APIs. Install the dependencies in `requirements.txt` in a compatible environment, then:

```sh
mkdir -p frames out
python3 main.py input.mp4
```

Output: `output.mp4`. Optional arguments control frame rate, render size and threads.
