(ns server.routes
  (:require [ring.util.response :refer [response resource-response]]
            [ring.middleware.json :as json]
            [compojure.core :refer [defroutes GET POST]]
            [compojure.handler :as handler]
            [compojure.route :as route]
            [server.db :as db]))

(defroutes app-routes

  (GET "/" []
    (resource-response "/html/index.html" {:root "public"}))

  (POST "/stand" []
    (response "standing..."))

  (route/resources "/")
  (route/not-found "Not Found"))

(def app
  (-> app-routes
      handler/site
      json/wrap-json-response))
