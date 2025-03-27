npm run build
mkdir -p static/images
sed -i 's/\/assets\//\/static\/assets\//g' static/index.html