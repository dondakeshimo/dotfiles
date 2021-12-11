FROM ruby:2.7.1

ARG dir="/app"
WORKDIR $dir

COPY Gemfile* .

RUN bundle install && \
    gem install solargraph

WORKDIR /app

ENTRYPOINT ["solargraph"]
CMD ["socket", "--host", "0.0.0.0", "--port", "7658"]
