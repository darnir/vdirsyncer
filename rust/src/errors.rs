use failure;

pub type Fallible<T> = Result<T, failure::Error>;

shippai_export!();

#[derive(Debug, Fail, Shippai)]
pub enum Error {
    #[fail(display = "The item cannot be parsed")]
    ItemUnparseable,

    #[fail(display = "Unexpected version {}, expected {}", found, expected)]
    UnexpectedVobjectVersion {
        found: String,
        expected: String,
    },

    #[fail(display = "Unexpected component {}, expected {}", found, expected)]
    UnexpectedVobject {
        found: String,
        expected: String,
    },

    #[fail(display = "Item '{}' not found", href)]
    ItemNotFound {
        href: String,
    },

    #[fail(display = "The href '{}' is already taken", href)]
    ItemAlreadyExisting {
        href: String,
    },

    #[fail(display = "A wrong etag for '{}' was provided. Another client's requests might \
                      conflict with vdirsyncer.",
           href)]
    WrongEtag {
        href: String,
    },

    #[fail(display = "The mtime for '{}' has unexpectedly changed. Please close other programs\
                      accessing this file.",
           filepath)]
    MtimeMismatch {
        filepath: String,
    },
}

pub unsafe fn export_result<V>(
    res: Result<V, failure::Error>,
    c_err: *mut *mut ShippaiError,
) -> Option<V> {
    match res {
        Ok(v) => Some(v),
        Err(e) => {
            *c_err = Box::into_raw(Box::new(e.into()));
            None
        }
    }
}
