import express from "express";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import fileUpload from "express-fileupload";
import { engine } from "express-handlebars";
import { router } from "./routes.js";
import { create } from 'express-handlebars';
import exphbs from 'express-handlebars';
import './utils/handlebarsHelpers.js';


const app = express();


app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static("public"));
app.use(fileUpload());


const hbs = create({
  extname: ".hbs",
  helpers: {
      eq: (a, b) => a === b, 
  },
});

app.engine(".hbs", hbs.engine);
app.set("view engine", ".hbs");
app.set("views", "./views");


app.use("/", router);


app.engine(".hbs", engine({ extname: ".hbs" }));
const listener = app.listen(process.env.PORT || 4000, function () {
  console.log(`Todolist started on http://localhost:${listener.address().port}`);
});