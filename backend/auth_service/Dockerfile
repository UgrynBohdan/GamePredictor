# cd backend/auth_service
# docker build -t auth_service .
# docker run -p 5002:5002 --name auth_service auth_service 

FROM python
WORKDIR /app
COPY . .
RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt --system
EXPOSE 5002

CMD ["python", "app.py"]