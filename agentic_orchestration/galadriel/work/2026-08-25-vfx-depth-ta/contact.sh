#!/bin/zsh
cd "$(dirname "$0")"
cd sheet2
files=(${(f)"$(ls *.png | grep -v OURS | sort)"})
n=${#files}
echo "tiling $n frames"
args=()
for f in $files; do args+=(-i "$f"); done
ffmpeg -v error -y $args -filter_complex "$(python3 -c "
import sys
n=$n
cols=5
rows=(n+cols-1)//cols
print(''.join(f'[{i}:v]scale=384:-2,pad=390:230:3:3:black[p{i}];' for i in range(n)) +
      ''.join(f\"{''.join(f'[p{r*cols+c}]' for c in range(cols) if r*cols+c<n)}hstack=inputs={min(cols,n-r*cols)}[r{r}];\" for r in range(rows)) +
      ''.join(f'[r{r}]' for r in range(rows)) + f'vstack=inputs={rows}[out]')")" -map "[out]" ../IMPACT-CONTACT-SHEET.png
echo "wrote IMPACT-CONTACT-SHEET.png"
