FROM ruby:2.7.1

COPY Gemfile* .

RUN bundle install && \
    gem install solargraph

WORKDIR /app

ENTRYPOINT ["solargraph"]
CMD ["socket", "--host", "0.0.0.0", "--port", "7658"]
