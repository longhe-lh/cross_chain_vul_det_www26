# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SwapPosted1, SwapBonded2
- **rel_chain**: RequestSignatureVerified, ReleaseSignatureVerified
- **det_chain**: SwapLocked1, SwapReleased2
### src_chain: initial_chain
- **事件**: SwapPosted1
  - 函数: postSwap
  - 关键操作: require(_postedSwaps[encodedSwap] == 0, "Swap already exists"), _checkRequestSignature(encodedSwap, r, s, v, initiator), _unsafeDepositToken(tokenForIndex[tokenIndex], initiator, amount, tokenIndex)
- **事件**: SwapBonded2
  - 函数: bondSwap
  - 关键操作: require(postedSwap > 1, "Swap does not exist"), require(_poolIndexFromPosted(postedSwap) == 0, "Swap bonded to another pool")
### rel_chain: relay_chain
- **事件**: RequestSignatureVerified
  - 函数: _checkRequestSignature
  - 关键操作: require(signer != address(0), "Signer cannot be empty address"), require(v == 27 || v == 28, "Invalid signature")
- **事件**: ReleaseSignatureVerified
  - 函数: _checkReleaseSignature
  - 关键操作: require(signer != address(0), "Signer cannot be empty address"), require(v == 27 || v == 28, "Invalid signature")
### det_chain: target_chain
- **事件**: SwapLocked1
  - 函数: lock
  - 关键操作: require(_lockedSwaps[swapId] == 0, "Swap already exists"), _checkRequestSignature(encodedSwap, r, s, v, initiator), _balanceOfPoolToken[poolTokenIndex] -= (_amountFrom(encodedSwap) - _feeForLp(encodedSwap))
- **事件**: SwapReleased2
  - 函数: release
  - 关键操作: require(lockedSwap != 0, "Swap does not exist"), require(recipient != address(0), "Recipient cannot be zero address"), _checkReleaseSignature(encodedSwap, recipient, r, s, v, initiator), _balanceOfPoolToken[_poolTokenIndexForOutToken(encodedSwap, 0)] += serviceFee
---
