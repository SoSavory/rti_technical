FROM ruby:3.2.0
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
WORKDIR /display
COPY Gemfile /display/Gemfile 
COPY Gemfile.lock /display/Gemfile.lock 
RUN bundle install
EXPOSE 3000
CMD ["rails", "server", "-b", "0.0.0.0"]