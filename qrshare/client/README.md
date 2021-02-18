# qrshare client

This is the client side for the sharing app qrshare.

## Development

Development is conducted with flask server and live reload provided by rollup

There are two ways to go about this

### All

```bash
yarn dev
```

### Specific page

```bash
yarn dev --config-[page]
```

**where:**

`[page]` is what page to build on change

For example:

```bash
yarn dev --config-main
```

## Deployment

Before the app qrshare is packaged, it is required that client side be build.

To build run the following code in this directory `qrshare/client`

```yarn
yarn build
```

or

```bash
npm run build
```
