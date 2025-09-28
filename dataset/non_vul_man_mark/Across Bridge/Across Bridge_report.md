# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: FundsDeposited1, RequestedSpeedUpDeposit2
- **rel_chain**: MessageRelayed, TokensRelayed
- **det_chain**: FilledRelay1, RequestedSpeedUpDeposit2
### src_chain: Ethereum
- **事件**: FundsDeposited1
  - 函数: deposit
  - 关键操作: require(enabledDepositRoutes[originToken][destinationChainId], "Disabled route"), require(relayerFeePct < 0.5e18, "invalid relayer fee"), require(getCurrentTime() >= quoteTimestamp - depositQuoteTimeBuffer && getCurrentTime() <= quoteTimestamp + depositQuoteTimeBuffer, "invalid quote time"), IERC20(originToken).safeTransferFrom(msg.sender, address(this), amount)
- **事件**: RequestedSpeedUpDeposit2
  - 函数: speedUpDeposit
  - 关键操作: require(newRelayerFeePct < 0.5e18, "invalid relayer fee"), _verifyUpdateRelayerFeeMessage(depositor, chainId(), newRelayerFeePct, depositId, depositorSignature), emit RequestedSpeedUpDeposit(newRelayerFeePct, depositId, depositor, depositorSignature)
### rel_chain: Arbitrum
- **事件**: MessageRelayed
  - 函数: relayMessage
  - 关键操作: uint256 requiredL1CallValue = _contractHasSufficientEthBalance(), l1Inbox.createRetryableTicket{ value: requiredL1CallValue }(target, 0, l2MaxSubmissionCost, l2RefundL2Address, l2RefundL2Address, l2GasLimit, l2GasPrice, message), emit MessageRelayed(target, message)
- **事件**: TokensRelayed
  - 函数: relayTokens
  - 关键操作: uint256 requiredL1CallValue = _contractHasSufficientEthBalance(), IERC20(l1Token).safeIncreaseAllowance(erc20Gateway, amount), l1ERC20GatewayRouter.outboundTransfer{ value: requiredL1CallValue }(l1Token, to, amount, l2GasLimit, l2GasPrice, data), emit TokensRelayed(l1Token, l2Token, amount, to)
### det_chain: Polygon
- **事件**: FilledRelay1
  - 函数: fillRelay
  - 关键操作: require(relayFills[relayHash] < relayData.amount, "relay filled"), fillAmountPreFees = _computeAmountPreFees(maxTokensToSend, (relayData.realizedLpFeePct + updatableRelayerFeePct)), IERC20(relayData.destinationToken).safeTransferFrom(msg.sender, relayData.recipient, amountToSend)
- **事件**: RequestedSpeedUpDeposit2
  - 函数: executeSlowRelayLeaf
  - 关键操作: require(MerkleLib.verifySlowRelayFulfillment(rootBundles[rootBundleId].slowRelayRoot, relayData, proof), "Invalid proof"), fillAmountPreFees = _fillRelay(relayHash, relayData, relayData.amount, 0, true), emit FilledRelay(relayData.amount, relayFills[relayHash], fillAmountPreFees, 0, relayData.originChainId, relayData.destinationChainId, relayData.relayerFeePct, 0, relayData.realizedLpFeePct, relayData.depositId, relayData.destinationToken, msg.sender, relayData.depositor, relayData.recipient, true)
---
