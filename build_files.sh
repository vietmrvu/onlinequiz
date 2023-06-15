# build_files.sh
pip install -r requirements.txt
python3.9 manage.py collectstatic
rm  -rf /vercel/path0/staticfiles