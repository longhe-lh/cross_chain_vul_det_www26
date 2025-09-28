# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SwapInitilaized1, SwapInitilaized2
- **rel_chain**: RedeemInitilaized
- **det_chain**: RedeemInitilaized1, RedeemInitilaized2
### src_chain: source_chain
- **事件**: SwapInitilaized1
  - 函数: swap
  - 关键操作: require(supportedChains[thisChainId] == true && supportedChains[chainTo] == true, "Bridge: One of the blockchains isn't supported"), IERC20(supportedTokens[symbol]).burnFrom(msg.sender, amount), usersNonces[msg.sender][nonce] = true
- **事件**: SwapInitilaized2
  - 函数: swap
  - 关键操作: require(supportedChains[thisChainId] == true && supportedChains[chainTo] == true, "Bridge: One of the blockchains isn't supported"), IERC20(supportedTokens[symbol]).burnFrom(msg.sender, amount), usersNonces[msg.sender][nonce] = true
### rel_chain: relay_chain
- **事件**: RedeemInitilaized
  - 函数: redeem
  - 关键操作: require(receiver == msg.sender, "Only receiver can call this function"), require(chainTo == thisChainId, "This transaction is for another chain"), bytes32 signedDataHash = keccak256(abi.encodePacked(receiver, supportedTokens[symbol], amount, nonce, time, chainTo)), address signer = message.recover(v, r, s), require(hasRole(VALIDATOR_ROLE, signer), "Bridge: invalid sig"), IERC20(supportedTokens[symbol]).mint(receiver, amount), usersNonces[msg.sender][nonce] == true
### det_chain: destination_chain
- **事件**: RedeemInitilaized1
  - 函数: redeem
  - 关键操作: require(receiver == msg.sender, "Only the receiver can collect the tokens"), require(chainTo == thisChainId, "This transaction is for another chain"), bytes32 signedDataHash = keccak256(abi.encode(receiver, supportedTokens[symbol], amount, nonce, chainTo)), address signer = message.recover(v, r, s), require(hasRole(VALIDATOR_ROLE, signer), "Bridge: invalid sig"), IERC20(supportedTokens[symbol]).mint(receiver, amount), usersNonces[msg.sender][nonce] = true
- **事件**: RedeemInitilaized2
  - 函数: redeem
  - 关键操作: require(receiver == msg.sender, "Only the receiver can collect the tokens"), require(chainTo == thisChainId, "This transaction is for another chain"), bytes32 signedDataHash = keccak256(abi.encode(receiver, token, chainTo, amount, nonce)), address signer = signedDataHash.toEthSignedMessageHash().recover(v, r, s), require(hasRole(VALIDATOR_ROLE, signer), "Bridge: invalid sig"), IERC20(token).mint(receiver, amount), usersNonces[receiver][nonce] = true
---
