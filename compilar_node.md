install nodeJS
https://nodejs.org/en/download/

edit `C:\venv\Lib\site-packages\superset\static\assets\package.json`

add commant to build on Windows (in "scripts")

<code>"build-windows": "SET \"NODE_ENV=production\" && webpack --colors --progress",</code>

first time install yarn and modules
<code>npm install
npm install yarn -g</code>

**build**
<code>npm run build-windows</code>

the output directory is:
C:\venv\Lib\site-packages\superset\static\assets\dist