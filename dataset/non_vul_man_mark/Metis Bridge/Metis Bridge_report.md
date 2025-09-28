# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: ERC20DepositInitiated1, ETHDepositInitiated2
- **rel_chain**: SentMessage, RelayedMessage, FailedRelayedMessage
- **det_chain**: ERC20WithdrawalFinalized1, ETHWithdrawalFinalized2
### src_chain: L1
- **事件**: ERC20DepositInitiated1
  - 函数: depositERC20
  - 关键操作: IERC20(_l1Token).safeTransferFrom(_from, address(this), _amount), sendCrossDomainMessageViaChainId(_chainId, l2TokenBridge, _l2Gas, message, msg.value)
- **事件**: ETHDepositInitiated2
  - 函数: depositETH
  - 关键操作: sendCrossDomainMessageViaChainId(_chainId, l2TokenBridge, _l2Gas, message, fee)
### rel_chain: CanonicalTransactionChain
- **事件**: SentMessage
  - 函数: sendMessageViaChainId
  - 关键操作: oracle.processL2SeqGas{value:msg.value}(msg.sender, _chainId), _sendXDomainMessageViaChainId(_chainId, canonicalTransactionChain, xDomainCalldata, _gasLimit)
- **事件**: RelayedMessage
  - 函数: relayMessageViaChainId
  - 关键操作: _verifyXDomainMessageByChainId(_chainId, xDomainCalldata, _proof), successfulMessages[xDomainCalldataHash] = true, (bool success, ) = _target.call(_message)
- **事件**: FailedRelayedMessage
  - 函数: relayMessageViaChainId
  - 关键操作: _verifyXDomainMessageByChainId(_chainId, xDomainCalldata, _proof), successfulMessages[xDomainCalldataHash] = true, (bool success, ) = _target.call(_message)
### det_chain: L2
- **事件**: ERC20WithdrawalFinalized1
  - 函数: finalizeERC20WithdrawalByChainId
  - 关键操作: deposits[_l1Token][_chainid][_l2Token] = deposits[_l1Token][_chainid][_l2Token] - _amount, IERC20(_l1Token).safeTransfer(_to, _amount)
- **事件**: ETHWithdrawalFinalized2
  - 函数: finalizeETHWithdrawalByChainId
  - 关键操作: (bool success, ) = _to.call{value: _amount}(new bytes(0)), require(success, "TransferHelper::safeTransferETH: ETH transfer failed")
---
