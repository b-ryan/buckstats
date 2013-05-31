(defproject server "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [ring/ring-json "0.2.0"]
                 [compojure "1.1.5"]
                 [org.postgresql/postgresql "9.2-1002-jdbc4"]
                 [korma "0.3.0-RC5"]
                 [clj-time "0.5.1"]]
  :plugins [[lein-ring "0.8.3"]]
  :ring {:handler server.routes/app}
  :profiles
  {:dev {:dependencies [[ring-mock "0.1.3"]]}})
