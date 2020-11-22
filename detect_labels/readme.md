## Usage

```
$ python3 safe_search.py [IMAGE_PATH]
```

## Example

Image: `sports.jpg` (Source image: [FORMAT](https://www.format.com/magazine/features/photography/sports-photographers))

![img](images/sports.jpg)

```
$ python3 detect_labels.py --source_image images/sports.jpg
```

Output:

```
Detecting labels from sports.jpg...

Found 5 labels
Player (99% confidence)
Football player (97% confidence)
Soccer player (95% confidence)
Games (94% confidence)
Tackle (94% confidence)
```

Image: `sports.jpg` (Source image: [wikiwand](https://www.wikiwand.com/id/Reog_(Ponorogo)))

![img](images/street.jpg)

```
$ python3 detect_labels.py --source_image images/street.jpg --max_results 8 
```

Output:
```
Detecting labels from street.jpg...

Found 8 labels
Street (94% confidence)
Alley (90% confidence)
Town (90% confidence)
Road (82% confidence)
Infrastructure (78% confidence)
Building (71% confidence)
City (67% confidence)
Neighbourhood (66% confidence)
```