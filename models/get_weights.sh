FILE=Udacity_Unet.pth
if [ ! -f "$FILE" ]; then
    echo "Downloading $FILE ..."
    # https://drive.google.com/file/d/1-S-xVyktQu67rRHKKsUXqMb1G8t1gLTM/view?usp=sharing
    gdown --id 1-S-xVyktQu67rRHKKsUXqMb1G8t1gLTM
else
    echo "$FILE Exist!"
    
fi