FROM python:3.10

WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

EXPOSE 8050

CMD ["streamlit", "run", "Introduction.py"]
