class Record < ApplicationRecord
    def self.summarize
        count = self.count 
        mean_cap_gains = self.sum(:capital_gain) / self.where("capital_gain != (?)", 0).count
        mean_cap_losses = self.sum(:capital_loss) / self.where("capital_loss != (?)", 0).count 
        response = {
            num_records: self.count,
            mean_cap_gains: mean_cap_gains,
            mean_cap_losses: mean_cap_losses,
            unique_professions: self.pluck(Arel.sql("count(distinct(occupation))")).first
        }
    end
end
