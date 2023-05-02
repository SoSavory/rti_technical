class RecordsController < ApplicationController

    def index
        @records = Record.offset(10 * params[:page].to_i).limit(10)
    end
end
