(ns server.db
  (:require [korma.core :refer :all]
            [korma.db :as db]))

(db/defdb stand (db/postgres {:db "stand"
                              :user "stand"
                              :password "password"
                              :host "127.0.0.1"}))

(defn latest-entry []
  (first
    (select "events"
      (fields :id :event :start_time :end_time)
      (order :id :DESC)
      (limit 1))))
