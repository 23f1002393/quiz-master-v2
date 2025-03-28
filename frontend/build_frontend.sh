npm run build
mkdir -p ../backend/static/images
cp public/favicon.ico ../backend/static/favicon.ico
sed -i 's/\/assets\//\/static\/assets\//g' ../backend/static/index.html