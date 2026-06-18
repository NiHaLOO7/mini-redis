FROM python:3.12-slim
WORKDIR /app
COPY . .
# RUN 
EXPOSE 6379
CMD ["python", "-m", "src.server"]