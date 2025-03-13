FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip
RUN python --version  # Kiểm tra phiên bản Python
RUN pip --version  # Kiểm tra phiên bản pip
EXPOSE 8000
RUN pip install --no-cache-dir -r requirements.txt
CMD gunicorn -w 4 -b 0.0.0.0 display_payment_app.app_flashsale:app