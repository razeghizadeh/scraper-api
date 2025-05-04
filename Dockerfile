# مرحله ساخت
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --user -r requirements.txt

# مرحله نهایی
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# اطمینان از اینکه اسکریپت‌ها در PATH هستند
ENV PATH=/root/.local/bin:$PATH

# پورت مورد استفاده توسط FastAPI
EXPOSE 8000

# دستور اجرا
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
