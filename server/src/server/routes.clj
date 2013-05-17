(ns server.routes
  (:require [ring.util.response :refer [response]]
            [ring.middleware.json :as json]
            [compojure.core :refer [defroutes GET POST]]
            [compojure.handler :as handler]
            [compojure.route :as route]
            [server.db :as db]))

(defroutes app-routes
  (GET "/" []
    (response (db/latest-entry)))
  (POST "/stand" []
    (response "coming..."))
  (route/resources "/")
  (route/not-found "Not Found"))

(def app
  (-> app-routes
      handler/site
      json/wrap-json-response))
