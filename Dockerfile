FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip
RUN python --version  # Kiểm tra phiên bản Python
RUN pip --version  # Kiểm tra phiên bản pip

RUN pip install --no-cache-dir -r requirements.txt
CMD gunicorn -w 4 -b 0.0.0.0:5000 display_payment_app.app_flashsale:app