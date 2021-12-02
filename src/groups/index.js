import { groups as tvm } from "./tvm.js";

const map = {
  tvm: tvm,
};

export default function getGroups(repo) {
  const result = [];
  if (!map[repo]) {
    console.error(`Unknown group repo ${repo}`);
    return [];
  }

  for (const group of map[repo]) {
    let obj = {};
    Object.assign(obj, group);
    result.push(obj);
  }

  return result;
}
