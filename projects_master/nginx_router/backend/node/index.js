// example file containing some config info or other code
const keys = require("./keys");

// Express app setup
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get("/api/v1", (req, res) => {
  res.send({ value: "Synth is running!!!" });
});

app.post("/api/v1/post", async (req, res) => {
  const data = req.body;

  if (data === "undefined") {
    return res.status(422).send("Example error response code!");
  }

  res.send({ got_data: data });
});

app.listen(5005, () => {
  console.log("Express app listening on port 5005");
});
