``source`` *(Path)*
    An existing path of a directory to traverse to find elligible files. Eligibility is defined from allowed extensions.

``--ext`` *(str)*
    This is for allowed file extensions. Only filenames ending with one of allowed extensions will be collected. You can use it multiple times to allow multiple extensions. If no extension is given then all files are collected. Do not start your extension pattern with their leading dot because it is already appended from code.

``--ignore-dir-lead`` *(str)*
    This is a leading pattern that will exclude paths starting with it. This is applied on the relative (to the 'source' path) directory path. Use it multiple time to define multiple pattern, a single match exclude a path.

``--ignore-file-lead`` *(str)*
    This is a leading pattern that will exclude files starting with it. This is applied on filename path. Use it multiple time to define multiple pattern, a single match exclude a path.

``--destination`` *(Path)*
    This is the path where to write file of collected files and their checksum. If it is not given the data will be printed to standard output.

``--format`` *(str)*
    This is the format to serialize data. JSON format is the one with the most informations.

``--help`` *(flag)*
    Display help message and exit
