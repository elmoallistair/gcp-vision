## Usage

```
$ python3 safe_search.py [-h] -i SOURCE_IMAGE
```

## Example

Image: `gtaiv.jpg` (Source image: [CNN](https://edition.cnn.com/2013/08/26/tech/gallery/top-violent-video-games/index.html))

![img](images/gtaiv.jpg)

```
$ python3 safe_search.py gtaiv.jpg
```

Output:
```
Detecting SafeSearch from gtaiv.jpg...

Safe Search
Adult    : VERY_UNLIKELY
Spoof    : UNLIKELY
Medical  : VERY_UNLIKELY
Violence : UNLIKELY
Racy     : VERY_UNLIKELY 
Likeliness values are Unknown, Very Unlikely, Unlikely, Possible, Likely, and Very Likely
```