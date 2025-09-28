# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: HomeGate
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: require(tokenContract != address(0x0), "should provide a token contract"), require(recipient == msg.sender, "should be the recipient"), _tokenStore.addHash(hash), require(v.length > 0, "should provide signatures at least one signature"), require(checkSignatures(hash, v.length, v, r, s) >= requiredOperators, "not enough signatures to proceed")
- **事件**: TokenRedeem2
  - 函数: redeem
  - 关键操作: require(tokenContract != address(0x0), "should provide a token contract"), require(value > 0, "should provide value"), require(transactionHash > 0, "TX hash should be provided"), bytes32 hash = prefixed(keccak256(abi.encodePacked(PREFIX, transactionHash, tokenContract, recipient, value))), hashStore.addHash(hash)
### rel_chain: OperatorHub
- **事件**: mint
  - 函数: mint
  - 关键操作: require(tokenContract != address(0x0), "should provide a token contract"), require(value > 0, "should provide value"), require(transactionHash > 0, "TX hash should be provided"), require(recipient == msg.sender, "should be the recipient"), ERC721Mintable(tokenContract).mint(recipient, value)
- **事件**: withdraw
  - 函数: withdraw
  - 关键操作: require(tokenContract != address(0x0), "should provide a token contract"), require(value > 0, "should provide value"), require(transactionHash > 0, "TX hash should be provided"), require(recipient == msg.sender, "should be the recipient"), ERC721Mintable(tokenContract).transfer(recipient, value)
### det_chain: ForeignGate
- **事件**: TokenWithdraw1
  - 函数: canWithdraw
  - 关键操作: require(tokenContract != address(0x0), "should provide a token contract"), require(recipient != address(0x0), "should provide a recipient"), require(value > 0, "should provide value"), require(transactionHash > 0, "TX hash should be provided")
- **事件**: TokenMint2
  - 函数: canMint
  - 关键操作: require(tokenContract != address(0x0), "should provide a token contract"), require(recipient != address(0x0), "should provide a recipient"), require(value > 0, "should provide value"), require(transactionHash > 0, "TX hash should be provided")
---
