# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Proposed1, Confirmed1
- **rel_chain**: Transfer
- **det_chain**: Transfer1
### src_chain: BSC or ETH
- **事件**: Proposed1
  - 函数: proposeTransaction
  - 关键操作: bytes32 message = prefixed(keccak256(abi.encodePacked(sender, receiver, amount)));, require(recoverSigner(message, signature) == proposer, "Signature Error: Not Signed by the Proposer");, require(potentialSigners.length == 3, "Three potential signers are required");, transactions[message] = Transaction(potentialSigners, new address[](0), sender, receiver, amount);, transactions[message].signers.push(msg.sender);
- **事件**: Confirmed1
  - 函数: confirmTransaction
  - 关键操作: bytes32 message = prefixed(keccak256(abi.encodePacked(sender, receiver, amount)));, require(recoverSigner(message, signature) == signer, "Signature Error: Not Signed by the Sender");, require(addressExists(transactions[message].potentialSigners, signer), "Provided Address is not a potential signer for this transaction");, require(!addressExists(transactions[message].signers, signer), "Sender has already signed this transaction");, transactions[message].signers.push(signer);, if (transactions[message].signers.length >= 2) { burn(trx.sender, trx.receiver, trx.amount); }
### rel_chain: Relay Chain
- **事件**: Transfer
  - 函数: burn
  - 关键操作: token.burn(from, amount);
### det_chain: BSC or ETH
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: token.mint(to, amount);
---
