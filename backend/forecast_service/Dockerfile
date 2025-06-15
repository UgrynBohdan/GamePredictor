# cd backend/forecast_service
# docker build -t forecast_service .
# docker run -p 5001:5001 --name forecast_service forecast_service

FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime
WORKDIR /app
COPY . .
RUN pip install uv
RUN uv pip install -r requirements.txt --system
EXPOSE 5001

CMD [ "python", "app.py" ]
