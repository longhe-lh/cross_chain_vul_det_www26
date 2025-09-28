# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Sent1, Burned2
- **rel_chain**: Voted, Signed, Executed
- **det_chain**: Minted1, Transfer2
### src_chain: Ethereum
- **事件**: Sent1
  - 函数: send
  - 关键操作: require(balanceOf[src] >= amount, "Dai/insufficient-balance");, if (src != msg.sender && allowance[src][msg.sender] != uint(-1)) { require(allowance[src][msg.sender] >= wad, "Dai/insufficient-allowance"); allowance[src][msg.sender] = sub(allowance[src][msg.sender], wad); }, balanceOf[src] = sub(balanceOf[src], wad);, balanceOf[dst] = add(balanceOf[dst], wad);
- **事件**: Burned2
  - 函数: burn
  - 关键操作: require(balanceOf[usr] >= wad, "Dai/insufficient-balance");, if (usr != msg.sender && allowance[usr][msg.sender] != uint(-1)) { require(allowance[usr][msg.sender] >= wad, "Dai/insufficient-allowance"); allowance[usr][msg.sender] = sub(allowance[usr][msg.sender], wad); }, balanceOf[usr] = sub(balanceOf[usr], wad);, totalSupply    = sub(totalSupply, wad);
### rel_chain: FederationChain
- **事件**: Voted
  - 函数: voteTransaction
- **事件**: Signed
  - 函数: executeTransaction
- **事件**: Executed
  - 函数: releaseTokensOnBridge
  - 关键操作: emit Voted(...);, bool acceptTransfer = bridge.acceptTransferAt(...);, require(acceptTransfer, "Federation: Bridge acceptTransfer error");
### det_chain: SideTokenChain
- **事件**: Minted1
  - 函数: mint
  - 关键操作: require(_msgSender() == minter, "SideToken: Caller is not the minter");
- **事件**: Transfer2
  - 函数: transfer
  - 关键操作: balances[msg.sender] = balances[msg.sender].sub(_value);, balances[_to] = balances[_to].add(sendAmount);
---
