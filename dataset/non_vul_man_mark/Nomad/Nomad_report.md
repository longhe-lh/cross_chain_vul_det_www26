# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Send1
- **rel_chain**: Dispatch, Update
- **det_chain**: Receive1
### src_chain: source_chain
- **事件**: Send1
  - 函数: send
  - 关键操作: require(_amount > 0, "!amnt");, require(_recipient != bytes32(0), "!recip");, IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);, _t.burn(msg.sender, _amount);
### rel_chain: relay_chain
- **事件**: Dispatch
  - 函数: dispatch
  - 关键操作: require(_messageBody.length <= MAX_MESSAGE_BODY_BYTES, "msg too long");, nonces[_destinationDomain] = _nonce + 1;, emit Dispatch(...);
- **事件**: Update
  - 函数: update
  - 关键操作: require(_oldRoot == committedRoot, "not current update");, confirmAt[_newRoot] = block.timestamp + optimisticSeconds;, committedRoot = _newRoot;
### det_chain: destination_chain
- **事件**: Receive1
  - 函数: handle
---
