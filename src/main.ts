import {marks} from "./front";
import {instrument} from "@shared/instrument";

instrument({
  marks,
  "title": "RESERVE DIAL",
  "primary": "Reserve Dial",
  "accent": "#64D8B6",
  "cadence": 60000,
  "motion": {enabled:false},
  "setup": "Start companion/serve.py"
});
