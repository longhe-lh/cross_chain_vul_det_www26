# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Send1, Relay1
- **rel_chain**: Relay
- **det_chain**: RelayDone1, Mint1
### src_chain: source_chain
- **事件**: Send1
  - 函数: send
  - 关键操作: require(_amount > minSend[_token], "amount too small"), require(maxSend[_token] == 0 || _amount <= maxSend[_token], "amount too large"), require(_maxSlippage > minimalMaxSlippage, "max slippage too small"), IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount)
- **事件**: Relay1
  - 函数: relay
  - 关键操作: require(transfers[transferId] == false, "transfer exists"), transfers[transferId] = true, _updateVolume(request.token, request.amount), if (delayThreshold > 0 && request.amount > delayThreshold), _addDelayedTransfer(transferId, request.receiver, request.token, request.amount), _sendToken(request.receiver, request.token, request.amount)
### rel_chain: relay_chain
- **事件**: Relay
  - 函数: verifySigs
### det_chain: destination_chain
- **事件**: RelayDone1
  - 函数: withdraw
  - 关键操作: require(withdraws[wdId] == false, "withdraw already succeeded"), withdraws[wdId] = true, _updateVolume(wdmsg.token, wdmsg.amount), if (delayThreshold > 0 && wdmsg.amount > delayThreshold), _addDelayedTransfer(wdId, wdmsg.receiver, wdmsg.token, wdmsg.amount), _sendToken(wdmsg.receiver, wdmsg.token, wdmsg.amount)
- **事件**: Mint1
  - 函数: mint
  - 关键操作: require(records[mintId] == false, "record exists"), records[mintId] = true, _updateVolume(request.token, request.amount), if (delayThreshold > 0 && request.amount > delayThreshold), _addDelayedTransfer(mintId, request.account, request.token, request.amount), IPeggedToken(request.token).mint(request.account, request.amount)
---
