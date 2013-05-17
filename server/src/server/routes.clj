(ns server.routes
  (:require [ring.util.response :refer [response]]
            [ring.middleware.json :as json]
            [compojure.core :refer [defroutes GET POST]]
            [compojure.handler :as handler]
            [compojure.route :as route]
            [korma.core :refer :all]
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

(defroutes app-routes
  (GET "/" []
    (response (latest-entry)))
  (POST "/stand" []
    (response "coming..."))
  (route/resources "/")
  (route/not-found "Not Found"))

(def app
  (-> app-routes
      handler/site
      json/wrap-json-response))
