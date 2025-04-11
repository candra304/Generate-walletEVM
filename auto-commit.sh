#!/bin/bash

echo -e "\n==============================="
echo "  SAT SET Git Auto Commit"
echo "        [by Chandra]"
echo -e "===============================\n"

read -p "GitHub Username     : " GH_USER
read -p "GitHub Token        : " GH_TOKEN
read -p "URL Repo GitHub     : " GH_REPO_URL
read -p "Pesan Commit        : " COMMIT_MSG

REPO_NAME=${PWD##*/}
README_FILE="README.md"

# ======== Deteksi file utama dan bahasa ========
PRIORITY_FILES=("main.py" "app.py" "index.js" "deploy.js" "deploy.sh")
for file in "${PRIORITY_FILES[@]}"; do
  if [ -f "$file" ]; then
    MAIN_FILE=$file
    break
  fi
done

if [ -z "$MAIN_FILE" ]; then
  MAIN_FILE=$(find . -type f \( -name "*.js" -o -name "*.py" -o -name "*.sh" \) | xargs ls -S 2>/dev/null | head -n 1)
fi

EXT="${MAIN_FILE##*.}"
case "$EXT" in
  js) LANGUAGE="Node.js";;
  py) LANGUAGE="Python";;
  sh) LANGUAGE="Bash";;
  *) LANGUAGE="Unknown";;
esac

# ======== Cek file dependensi ========
HAS_REQ=false
if [ -f "requirements.txt" ]; then
  DEP_FILE="requirements.txt"
  DEP_CONTENT=$(cat requirements.txt)
  HAS_REQ=true
elif [ -f "package.json" ]; then
  DEP_FILE="package.json"
  DEP_CONTENT=$(jq '.dependencies' package.json) 2>/dev/null
  HAS_REQ=true
elif ls *.js >/dev/null 2>&1; then
  DEP_FILE="*.js"
  DEP_CONTENT="(Tidak ada file package.json, dependencies tidak terdeteksi otomatis)"
  HAS_REQ=true
fi

# ======== Generate README.md ========
if [ ! -f $README_FILE ]; then
  echo "# $REPO_NAME" > $README_FILE
  echo -e "\nScript ini dibuat menggunakan **$LANGUAGE**." >> $README_FILE
  echo -e "\n## File Utama: \`$MAIN_FILE\`" >> $README_FILE
  echo -e "\n## Struktur Folder:" >> $README_FILE
  echo '```' >> $README_FILE
  tree -L 2 -I 'node_modules|__pycache__' >> $README_FILE 2>/dev/null || ls >> $README_FILE
  echo '```' >> $README_FILE
else
  echo -e "\nMenambahkan log perubahan ke README.md..."
fi

# ======== Tambah file dependency ========
if [ "$HAS_REQ" = true ]; then
  echo -e "\n## Dependency File: \`$DEP_FILE\`" >> $README_FILE
  echo '```' >> $README_FILE
  echo "$DEP_CONTENT" >> $README_FILE
  echo '```' >> $README_FILE
fi

# ======== Tambahkan perubahan terakhir ke README.md ========
echo -e "\n## Perubahan Terbaru:" >> $README_FILE
echo '```diff' >> $README_FILE
git diff --cached >> $README_FILE
echo '```' >> $README_FILE

# ======== Git Init & Push ========
if [ ! -d .git ]; then
  git init
  git branch -M main
fi

git add .
git commit -m "$COMMIT_MSG"
git remote remove origin 2>/dev/null
git remote add origin https://$GH_USER:$GH_TOKEN@$GH_REPO_URL

echo -e "\nPush ke GitHub..."
git push -u origin main

echo -e "\n✅ Project $REPO_NAME berhasil dipush ke GitHub!"

