(ns server.db
  (:require [korma.core :refer :all]
            [korma.db :as db]))

(db/defdb stand (db/postgres {:db "stand"
                              :user "stand"
                              :password "password"
                              :host "127.0.0.1"}))

(defn- latest []
  (first
    (select "events"
      (fields :id :event :start_time :end_time)
      (order :id :DESC)
      (limit 1))))

(defn get-events [& [lim]]
  (if lim (select "events" (order :id :DESC) (limit lim))
          (select "events" (order :id :DESC))))

(defn start-event [event]
  (let [latest (latest)]
    (if latest
      "change latest"
      "start a new one")))
