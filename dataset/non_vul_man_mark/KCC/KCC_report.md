# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: DepositNative1, DepositToken2
- **rel_chain**: WithdrawingNative, WithdrawingToken
- **det_chain**: WithdrawDoneNative1, WithdrawDoneToken2
### src_chain: source_chain
- **事件**: DepositNative1
  - 函数: depositNative
  - 关键操作: require(msg.value >= swapFee, "Bridge:insufficient swap fee"), payable(feeTo).transfer(swapFee), emit DepositNative(msg.sender, msg.value - swapFee, _targetAddress, chain, swapFee)
- **事件**: DepositToken2
  - 函数: depositToken
  - 关键操作: require(msg.value == swapFee, "Bridge:swap fee not equal"), payable(feeTo).transfer(swapFee), (status, returnedData) = token.call(abi.encodeWithSignature("transferFrom(address,address,uint256)", _from, this, _value)), require(status && (returnedData.length == 0 || abi.decode(returnedData, (bool))), 'Bridge:deposit failed')
### rel_chain: relay_chain
- **事件**: WithdrawingNative
  - 函数: withdrawNative
  - 关键操作: require(address(this).balance >= value, "Bridge:not enough native token"), require(taskHash == keccak256((abi.encodePacked(to, value, proof))), "Bridge:taskHash is wrong"), require(!filledTx[taskHash], "Bridge:tx filled already"), uint256 status = logic.supportTask(logic.WITHDRAWTASK(), taskHash, msg.sender, operatorRequireNum), to.transfer(value), filledTx[taskHash] = true, logic.removeTask(taskHash)
- **事件**: WithdrawingToken
  - 函数: withdrawToken
  - 关键操作: require(taskHash == keccak256((abi.encodePacked(to, value, proof))), "Bridge:taskHash is wrong"), require(!filledTx[taskHash], "Bridge:tx filled already"), uint256 status = logic.supportTask(logic.WITHDRAWTASK(), taskHash, msg.sender, operatorRequireNum), filledTx[taskHash] = true, logic.removeTask(taskHash)
### det_chain: destination_chain
- **事件**: WithdrawDoneNative1
  - 函数: withdrawNative
  - 关键操作: emit WithdrawDoneNative(to, value, proof)
- **事件**: WithdrawDoneToken2
  - 函数: withdrawToken
  - 关键操作: emit WithdrawDoneToken(to, _token, value, proof)
---
