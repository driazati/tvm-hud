// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { Component, Fragment } from "react";
import { AiFillGithub } from "react-icons/ai";
import { Link } from "react-router-dom";
import AuthorizeGitHub from "./AuthorizeGitHub";

export default class Links extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showMore: false,
    };
  }

  render() {
    let more = null;
    if (this.state.showMore) {
      more = null;
    }
    return (
      <div className="links-container">
        <div className="Links">
          <div style={{ display: "inline" }}>
            <a style={{ fontWeight: "bold" }} href="https://hud.pytorch.org">
              TVM CI HUD
            </a>
            <ul style={{ display: "inline" }} className="menu">
              {["pytorch"].map((e) => (
                <Fragment key={e}>
                  {["main", "v0.5", "v0.6", "v0.7", "v0.8"].map((branch) => (
                    <li key={`${branch}`}>
                      <Link to={`/ci/apache/tvm/${branch}`}>{branch}</Link>
                    </li>
                  ))}
                </Fragment>
              ))}
              {/* <li>
                <a href="/overview">overview</a>
              </li> */}
              {/* <li>
                <a
                  href="more"
                  onClick={(e) => {
                    e.preventDefault();
                    const prev = this.state.showMore;
                    this.setState({ showMore: !prev });
                    return false;
                  }}
                >
                  {this.state.showMore ? "less" : "more"}
                </a>
              </li> */}
            </ul>
          </div>
          <div
            style={{
              display: "inline",
              marginLeft: "auto",
              marginRight: "0px",
            }}
          >
            <ul style={{ marginBottom: "0" }} className="menu">
              <li>
                <a href="https://github.com/pytorch/pytorch/wiki/Using-hud.pytorch.org">
                  help
                </a>
              </li>
              <li>
                <a href="https://github.com/pytorch/ci-hud/issues/new?assignees=&labels=&template=feature_request.yaml&title=%5Bfeature%5D%3A+">
                  requests
                </a>
              </li>
              <li>
                <AuthorizeGitHub />
              </li>
              <li>
                <a
                  style={{ color: "black" }}
                  href="https://github.com/pytorch/pytorch-ci-hud"
                >
                  <AiFillGithub />
                </a>
              </li>
            </ul>
          </div>
        </div>
        {more}
      </div>
    );
  }
}
