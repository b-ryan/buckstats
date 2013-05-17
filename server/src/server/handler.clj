(ns server.handler
  (:require [ring.util.response :refer [response]]
            [ring.middleware.json :as json]
            [compojure.core :refer [defroutes GET POST]]
            [compojure.handler :as handler]
            [compojure.route :as route]
            [korma.core]
            [korma.db :as db]))

(db/defdb stand (db/postgres {:db "stand"
                              :user "stand"
                              :password "password"
                              :host "127.0.0.1"}))

(defroutes app-routes
  (GET "/" []
    (response (korma.core/select "events")))
  (POST "/stand" []
    (response "coming..."))
  (route/resources "/")
  (route/not-found "Not Found"))

(def app
  (-> app-routes
      handler/site
      json/wrap-json-response))
